% hard3_0041  eq1=256 eq2=2477  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(X,X),X),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(f(Y,Z),X)),Y) )).
