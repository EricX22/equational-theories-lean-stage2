% hard3_0276  eq1=2651 eq2=3933  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,X),f(Y,X)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(X,f(Y,Z)),W) )).
