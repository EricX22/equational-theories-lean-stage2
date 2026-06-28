% hard3_0201  eq1=1852 eq2=3089  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(Y,X)),f(Y,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(X,Y),Z),Y),X) )).
