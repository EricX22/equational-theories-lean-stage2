% hard3_0260  eq1=2478 eq2=2287  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(f(Y,Z),X)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,f(Y,f(Z,W))),Z) )).
