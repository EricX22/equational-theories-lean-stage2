% order5v2_0342  eq1=16546 eq2=13124  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(f(Y,Z),Y),Y),Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(X,f(Y,W))),Z)) )).
