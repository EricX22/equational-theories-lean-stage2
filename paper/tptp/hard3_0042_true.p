% hard3_0042  eq1=258 eq2=851  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(X,X),Y),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(f(Y,Y),f(Z,W))) )).
