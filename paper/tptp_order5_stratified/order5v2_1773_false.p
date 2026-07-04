% order5v2_1773  eq1=22804 eq2=61339  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(f(W,Z),W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Z) != f(f(X,f(X,Z)),W) )).
