% hard3_0134  eq1=1057 eq2=329  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Z,X)),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(Z,Y)) )).
