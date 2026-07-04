% order5_0174  eq1=59780 eq2=8159  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(Z,f(f(W,X),Y)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,f(W,W)),U))) )).
