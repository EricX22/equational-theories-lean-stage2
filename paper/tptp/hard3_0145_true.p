% hard3_0145  eq1=1181 eq2=1289  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(Z,X)),Y)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(f(f(X,Y),Y),Y)) )).
