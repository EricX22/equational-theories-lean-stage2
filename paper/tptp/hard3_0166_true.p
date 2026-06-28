% hard3_0166  eq1=1487 eq2=287  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,X),f(X,f(Z,W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Y),Z),Y) )).
