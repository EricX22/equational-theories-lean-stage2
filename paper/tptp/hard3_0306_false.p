% hard3_0306  eq1=2871 eq2=855  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,f(Y,X)),Z),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(Y,Z),f(X,W))) )).
