% order5_0227  eq1=44595 eq2=21011  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(Y,f(f(Z,f(X,Y)),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(f(X,Y),Z),X)) )).
