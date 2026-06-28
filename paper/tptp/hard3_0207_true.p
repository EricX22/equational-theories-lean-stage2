% hard3_0207  eq1=1943 eq2=4023  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(Y,Z)),f(X,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Z,f(Z,X)),Y) )).
