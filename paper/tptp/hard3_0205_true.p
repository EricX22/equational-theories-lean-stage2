% hard3_0205  eq1=1890 eq2=3873  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(X,X)),f(Z,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(X,f(Y,Z)),X) )).
