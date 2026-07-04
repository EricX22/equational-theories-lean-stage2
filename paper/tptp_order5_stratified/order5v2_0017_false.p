% order5v2_0017  eq1=43976 eq2=57939  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(Z,f(f(Z,Z),f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(f(f(Y,Z),Z),X) )).
