% order5v2_0848  eq1=26417 eq2=47401  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,Z),X)),f(W,W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Z,Y),f(f(Y,Z),W)) )).
