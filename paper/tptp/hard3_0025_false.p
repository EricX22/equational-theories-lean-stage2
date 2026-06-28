% hard3_0025  eq1=124 eq2=1776  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(f(Y,X),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,Z),f(f(Y,Y),X)) )).
