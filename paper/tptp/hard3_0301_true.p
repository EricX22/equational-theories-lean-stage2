% hard3_0301  eq1=2851 eq2=109  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,f(X,X)),Y),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(Y,Y),Z)) )).
