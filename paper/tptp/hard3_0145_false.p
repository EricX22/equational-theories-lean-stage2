% hard3_0145  eq1=1181 eq2=1289  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(Z,X)),Y)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(f(f(X,Y),Y),Y)) )).
