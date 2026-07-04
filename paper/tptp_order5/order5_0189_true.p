% order5_0189  eq1=35409 eq2=16942  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(X,f(X,Y)),f(X,Y)),Y) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(f(Z,W),U),Y),X)) )).
