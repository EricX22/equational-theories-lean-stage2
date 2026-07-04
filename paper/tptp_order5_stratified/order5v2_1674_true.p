% order5v2_1674  eq1=36939 eq2=54570  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Z),f(X,W)),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(W,f(Y,f(X,Y))) )).
