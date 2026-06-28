% hard3_0181  eq1=1603 eq2=2733  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(Y,Y),f(X,X)),X) )).
