% order5v2_1701  eq1=26971 eq2=39578  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,X),f(Z,W)),f(U,W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(Y,Z),f(Z,Y)),Y),X) )).
