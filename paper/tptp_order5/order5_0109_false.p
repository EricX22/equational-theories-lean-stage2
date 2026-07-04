% order5_0109  eq1=56488 eq2=45673  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,f(X,X)) = f(f(Y,f(Z,W)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(Z,f(f(f(Y,W),X),W)) )).
