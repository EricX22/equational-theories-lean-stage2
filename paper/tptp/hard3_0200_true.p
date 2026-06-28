% hard3_0200  eq1=1845 eq2=1856  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(X,Y)),f(Z,Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(Y,X)),f(Z,W)) )).
