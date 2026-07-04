% order5v2_0433  eq1=22886 eq2=59028  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,Y)),f(f(W,W),W)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(f(X,Y),Z) != f(W,f(W,f(U,Z))) )).
