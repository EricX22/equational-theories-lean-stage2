% order5v2_0653  eq1=29144 eq2=62055  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),Y),f(Y,W)) )).
fof(goal, conjecture, ! [X,Y] : ( f(f(X,Y),Y) = f(f(f(X,X),X),Y) )).
