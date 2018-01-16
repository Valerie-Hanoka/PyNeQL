#!/usr/bin/perl

use strict;
use warnings;
use File::Slurp;

# Quick and dirty tes file generator
# usage: perl generate_test_file.pl Thing

######################################################################
# Finding supported endpoints
######################################################################
sub list_endpoints{
    my @edpts = ();
    my $endpoints_file = "./pyneql/utils/endpoints.py";
    if (open(my $fh, '<:encoding(UTF-8)', $endpoints_file)) {
        while (my $row = <$fh>) {
            chomp $row;
            next if ($row =~/^\s*#|DEFAULT/ || not $row=~/= u'http/);
            $row =~s/\s*([a-zA-Z_]+)\s*=.*/$1/g;
            push @edpts, $row;
        }
    }
    return \@edpts;
}
my @endpoints = @{list_endpoints()};



######################################################################
# Generating test files for the ontology classes passed as parameter #
######################################################################

foreach my $class_name (@ARGV) {
    my $ontology_file = "./pyneql/ontology/$class_name.py";

    my @functions = ();
    my @class_variables = ();

    if (open(my $fh, '<:encoding(UTF-8)', $ontology_file)) {
        while (my $row = <$fh>) {
            chomp $row;
            next if ($row=~/^\s*#.*/);
            push @functions, $row if ($row=~/^\s*def [^_]/);
            push @class_variables, $row if ($row=~/^\s*has_/);
        }
    }

    # Cleaning class variables and transforming them into an argument string
    @class_variables = map { s/^\s*has_([^\s]*)\s*=.*/$1="XXX"/; $_ } @class_variables;
    my $class_variables_str = join ', ', @class_variables;


    # Printing the preamble
    print <<"PREAMBLE_END";
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import *

from pyneql.ontology.${class_name} import ${class_name}
OTHER IMPORTS
PREAMBLE_END

    # printing functions
    for my $function (@functions){

        $function =~ s/\s*def\s*([^\(]*).*/$1/;
        my $test_template = generate_test_function_for_function($class_name, $class_variables_str, $function);

    }
}

sub generate_test_function_for_function{
    my ($class_name, $class_variables_str, $function_definition) = @_;
    my $lc_class_name = lc $class_name;
    my $test_function = "";

    # Query function should be tested for all endpoints, with strict
    # and non-strict modes
    if ($function_definition =~/ query\(/){
        my @modes = qw/True False/;
        for my $endpoint (@endpoints){
            $test_function = $test_function."\n# Testing Endpoint: $endpoint\n";
            for my $mode (@modes){
                my $tmp = <<"END_TMP";
def test_${lc_class_name}_${endpoint}_${function_definition}_strict_${mode}():
    \"\"\"${class_name} - ${endpoint} - strict=${mode} - : Should {pass|fail} \"\"\"
    ${lc_class_name} = ${class_name}(${class_variables_str})
    ${lc_class_name}.add_query_endpoint(Endpoint.${endpoint})
    ${lc_class_name}.query(strict_mode=${mode})
    assert

END_TMP
                $test_function = $test_function.$tmp;
            }

        }
    }
    else{
        $test_function = <<"END_TXT";
def test_${lc_class_name}_${function_definition}():
    \"\"\"${class_name} - : Should {pass|fail} \"\"\"
    ${lc_class_name} = ${class_name}(${class_variables_str})
    ${lc_class_name}.add_query_endpoints([Endpoint.XXX])
    ${lc_class_name}.query(strict_mode=True)
    result = ${lc_class_name}.${function_definition}()
    assert result ==
END_TXT
        }

    print $test_function."\n";
    return "None";
}



