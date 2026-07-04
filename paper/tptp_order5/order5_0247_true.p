% order5_0247  eq1=33872 eq2=48966  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,X),f(X,f(Z,W))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(Y,Y),Z),f(Z,Z)) )).
