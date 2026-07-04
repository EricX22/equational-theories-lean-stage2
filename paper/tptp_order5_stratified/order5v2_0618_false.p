% order5v2_0618  eq1=20435 eq2=28074  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,f(W,W)),Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(Y,f(Z,X)),W),f(U,Y)) )).
