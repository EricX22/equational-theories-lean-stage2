% hard3_0374  eq1=3745 eq2=377  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(W,Z)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(X,Y),X) )).
