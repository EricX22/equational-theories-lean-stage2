% hard3_0203  eq1=1882 eq2=4125  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(X,f(Y,Z)),f(W,W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(X,X),Z),Z) )).
