% hard3_0026  eq1=127 eq2=2148  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(f(Y,Y),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,Y),Z),f(Y,X)) )).
