% order5v2_0104  eq1=36794 eq2=22598  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(Y,Z),X),f(Y,Y)),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Y,X)),f(f(X,Z),W)) )).
