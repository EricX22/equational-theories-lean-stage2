% order5v2_0396  eq1=34163 eq2=54698  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(X,f(Y,Y))),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(X,X)) != f(X,f(f(Y,Z),W)) )).
