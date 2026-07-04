% order5v2_1793  eq1=47244 eq2=43299  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(Y,Z),f(f(Y,Z),X)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(X,f(f(Y,X),f(X,Y))) )).
