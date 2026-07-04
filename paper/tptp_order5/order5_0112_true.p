% order5_0112  eq1=48288 eq2=51048  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(Z,f(Y,Z)),f(Y,X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(f(W,X),Z)),W) )).
