% hard3_0274  eq1=2645 eq2=2287  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(X,X),f(X,X)),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,f(Y,f(Z,W))),Z) )).
