% order5v2_0412  eq1=790 eq2=57949  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(Z,W),U))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(f(Y,W),X),Y) )).
