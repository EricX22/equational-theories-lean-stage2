% order5v2_0887  eq1=52514 eq2=3970  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(f(Y,f(Z,Y)),W),U) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Y,f(Y,Z)),W) )).
