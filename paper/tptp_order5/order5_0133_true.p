% order5_0133  eq1=45411 eq2=29005  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Y,f(f(f(X,Z),X),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),Z),f(W,W)) )).
