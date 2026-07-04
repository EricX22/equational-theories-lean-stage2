% order5v2_1144  eq1=19888 eq2=14109  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,X),f(f(Z,f(X,Y)),W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(f(Y,W),Z)),Y)) )).
