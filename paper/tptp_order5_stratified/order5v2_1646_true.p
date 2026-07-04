% order5v2_1646  eq1=51653 eq2=48568  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Y,Z),f(Z,W)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(f(X,Y),X),f(Z,Z)) )).
