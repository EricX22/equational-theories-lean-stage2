% order5v2_1017  eq1=9697 eq2=45299  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,Y),f(Z,f(X,Y)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(f(Y,Z),X),Z)) )).
