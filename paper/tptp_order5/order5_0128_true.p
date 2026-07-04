% order5_0128  eq1=31163 eq2=1642  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),f(Y,W))),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,X),f(f(Y,Z),Z)) )).
