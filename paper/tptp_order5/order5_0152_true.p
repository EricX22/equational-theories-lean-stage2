% order5_0152  eq1=54692 eq2=45270  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( f(X,f(X,X)) = f(X,f(f(Y,Y),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(f(X,Z),Z),Z)) )).
