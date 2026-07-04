% order5v2_0251  eq1=35032 eq2=41624  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(f(X,X),W)),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(Y,f(Y,f(X,f(Z,X)))) )).
