% order5_0077  eq1=33344 eq2=5586  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(f(Z,Y),X),X)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(X,f(X,f(f(Y,Z),W)))) )).
