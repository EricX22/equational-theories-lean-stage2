% order5v2_0814  eq1=26116 eq2=23422  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,X),Y)),f(Z,W)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(Y,X),Z),f(Y,f(W,U))) )).
