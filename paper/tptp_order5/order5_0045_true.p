% order5_0045  eq1=47077 eq2=51857  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(f(X,Z),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(Z,Z),f(Y,Y)),Y) )).
