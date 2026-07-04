% order5_0198  eq1=3780 eq2=48556  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(Y,Z),f(W,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(f(X,X),Y),f(Z,X)) )).
