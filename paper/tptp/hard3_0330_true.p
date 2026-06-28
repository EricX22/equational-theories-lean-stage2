% hard3_0330  eq1=3086 eq2=2262  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(X,Y),Z),X),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(Y,f(X,Z))),W) )).
