% hard3_0210  eq1=1970 eq2=2063  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(X,Y),Y),f(Y,X)) )).
